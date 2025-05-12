extern crate uom;

use std::fmt::{Display, Formatter, Error};
use std::ops::{Add, Div, Mul, Sub, Neg};
use uom::fmt::DisplayStyle::Abbreviation;
use uom::si::f32::{Angle, Area, Length, Mass, Time, Velocity, Momentum, Ratio};
use uom::si::angle::degree;
use uom::si::area::square_meter;
use uom::si::length::{micrometer, millimeter, meter};
use uom::si::mass::gram;
use uom::si::time::{second, millisecond, microsecond, nanosecond};
use uom::si::ratio::ratio;
use uom::si::velocity::{meter_per_second};
// use uom::si::momentum::kilogram_meter_per_second;


#[derive(Clone, Copy)]
struct Vec3d<T> {
    x: T,
    y: T,
    z: T
}


impl Vec3d<Length> {
    pub fn abs(&self) -> Length {
        (self.x * self.x + self.y * self.y + self.z * self.z).sqrt()
    }
}


impl Vec3d<Area> {
    pub fn abs(&self) -> Area {
        (self.x * self.x + self.y * self.y + self.z * self.z).sqrt()
    }
}


impl<T: Add<Output = T>> Add for Vec3d<T> {
    type Output = Vec3d<T>;

    fn add(self, rhs: Vec3d<T>) -> Vec3d<T> {
        Self {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
            z: self.z + rhs.z,
        }
    }
}


impl<T: Sub<Output = T>> Sub for Vec3d<T> {
    type Output = Vec3d<T>;

    fn sub(self, rhs: Vec3d<T>) -> Vec3d<T> {
        Self {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
            z: self.z - rhs.z,
        }
    }
}

impl<T: Neg<Output = T>> Neg for Vec3d<T> {
    type Output = Vec3d<T>;

    fn neg(self) -> Vec3d<T> {
        Self {
            x: -self.x,
            y: -self.y,
            z: -self.z,
        }
    }
}


impl<R: Copy, S, T: Mul<R, Output = S>> Mul<R> for Vec3d<T> {
    type Output = Vec3d<S>;

    fn mul(self, rhs: R) -> Vec3d<S> {
        Self::Output {
            x: self.x * rhs,
            y: self.y * rhs,
            z: self.z * rhs,
        }
    }
}


impl<R: Copy, S, T: Div<R, Output = S>> Div<R> for Vec3d<T> {
    type Output = Vec3d<S>;

    fn div(self, rhs: R) -> Vec3d<S> {
        Self::Output {
            x: self.x / rhs,
            y: self.y / rhs,
            z: self.z / rhs,
        }
    }
}


fn dot(a: Vec3d<Length>, b: Vec3d<Length>) -> Length {
    (a.x * b.x + a.y * b.y + a.z * b.z).sqrt()
}


fn cross(a: Vec3d<Length>, b: Vec3d<Length>) -> Vec3d<Area> {
    Vec3d::<Area> {
        x: a.y * b.z - a.z * b.y,
        y: a.z * b.x - a.x * b.z,
        z: a.x * b.y - a.y * b.x,
    }
}


type Position3d = Vec3d<Length>;
type Velocity3d = Vec3d<Velocity>;
type Momentum3d = Vec3d<Momentum>;


struct PhysicalObject {
    mass: Mass,
    position: Position3d,
    velocity: Velocity3d,
}


impl PhysicalObject {
    fn next_pos(&self, config: &Config) -> Position3d{
        self.position + self.velocity * config.timestep
    }

    fn update_pos(&mut self, config: &Config) {
        self.position = self.next_pos(config);
    }

    fn momentum(&self) -> Momentum3d {
        self.velocity * self.mass
    }
}


impl Display for PhysicalObject {
    fn fmt(&self, formatter: &mut Formatter) -> Result<(), Error> {
        write!(formatter, "pos: {}, speed: {}", self.position, self.velocity)
    }
}


impl Display for Position3d {
    fn fmt(&self, formatter: &mut Formatter) -> Result<(), Error> {
        write!(
            formatter,
            "({}, {}, {})",
            self.x.into_format_args(millimeter, Abbreviation),
            self.y.into_format_args(millimeter, Abbreviation),
            self.z.into_format_args(millimeter, Abbreviation) 
        )
    }
}


impl Display for Velocity3d {
    fn fmt(&self, formatter: &mut Formatter) -> Result<(), Error> {
        write!(
            formatter,
            "({}, {}, {})",
            self.x.into_format_args(meter_per_second, Abbreviation),
            self.y.into_format_args(meter_per_second, Abbreviation),
            self.z.into_format_args(meter_per_second, Abbreviation)
        )
    }
}


fn fully_transfer_momentum(a: &mut PhysicalObject, b: &mut PhysicalObject) {
    let mom_a = a.momentum();
    let mom_b = b.momentum();
    b.velocity = mom_a / a.mass;
    a.velocity = mom_b / b.mass;
}


fn detect_imminent_collision(a: &PhysicalObject, b: &PhysicalObject, config: &Config) -> bool {
    //TODO make reference_dist a little smaller and make sub time steps in case a collision is
    //possible
    let reference_dist = Length::new::<meter>(1e-8);
    let a_b = b.position - a.position;
    let step_a = a.velocity * config.timestep;
    let step_b = b.velocity * config.timestep;
    let step_max = (step_b - step_a).abs();
    let current_dist = a_b.abs();
    let subwrite_period = Ratio::new::<ratio>(0.1);
    if step_max >= current_dist {
        println!("Possible collision!");
        let substep = current_dist / step_max / 10.0;
        println!("substep size: {}", substep.into_format_args(ratio, Abbreviation));
        let mut ratio_of_t  = Ratio::new::<ratio>(0.0);
        let mut sub_a = a.position;
        let mut sub_b = b.position;
        let full_ratio = Ratio::new::<ratio>(1.0);
        while ratio_of_t < full_ratio {
            sub_a = sub_a + (step_a * ratio_of_t);
            sub_b = sub_b + (step_b * ratio_of_t);
            let distance = (sub_b - sub_a).abs();
            println!("substep: {}, dist: {}", ratio_of_t.into_format_args(ratio, Abbreviation), distance.into_format_args(micrometer, Abbreviation));
            if distance < reference_dist {
                return true
            }
            ratio_of_t += substep;
        }
        let end_dist = (a_b + step_b - step_a).abs();
        end_dist < reference_dist
    } else {
        false
    }
}


struct Ball {
    diameter: Length,
    phys: PhysicalObject
}


struct Bat {
    orientation: Vec<Angle>,
    phys: PhysicalObject
}


struct Config {
    duration: Time,
    timestep: Time,
    write_period: Time,
}


fn main() {
    let mut tt_ball = Ball{
        diameter: Length::new::<millimeter>(40.0),
        phys: PhysicalObject{
            mass: Mass::new::<gram>(2.7),
            position: Position3d {
                x: Length::new::<meter>(0.0),
                y: Length::new::<meter>(0.0),
                z: Length::new::<meter>(0.0)
            },
            velocity: Velocity3d{                
                x: Velocity::new::<meter_per_second>(0.0),
                y: Velocity::new::<meter_per_second>(0.0),
                z: Velocity::new::<meter_per_second>(0.0)
            }
        }
    };
    let mut bat = Bat{
        orientation: vec![
            Angle::new::<degree>(0.0),
            Angle::new::<degree>(0.0),
            Angle::new::<degree>(0.0)
        ],
        phys: PhysicalObject{
            mass: Mass::new::<gram>(150.0),
            position: Position3d{
                x: Length::new::<meter>(-0.1),
                y: Length::new::<meter>(0.0),
                z: Length::new::<meter>(0.0)
            },
            velocity: Velocity3d{
                x: Velocity::new::<meter_per_second>(1.0),
                y: Velocity::new::<meter_per_second>(0.0),
                z: Velocity::new::<meter_per_second>(0.0)
            }
        }
    };
    let config = Config{
        duration: Time::new::<second>(2.0),
        timestep: Time::new::<microsecond>(1.0),
        write_period: Time::new::<millisecond>(100.0)
    };

    let mut time = Time::new::<nanosecond>(0.0);

    while time <= config.duration {
        if detect_imminent_collision(&bat.phys, &tt_ball.phys, &config) {
            println!("collision detected at t = {}", time.into_format_args(microsecond, Abbreviation));
            println!(
                "time: {} | Ball: [{}] | Bat [{}]",
                time.into_format_args(microsecond, Abbreviation),
                tt_ball.phys,
                bat.phys,
            );
            fully_transfer_momentum(&mut bat.phys, &mut tt_ball.phys);
        }
        tt_ball.phys.update_pos(&config);
        bat.phys.update_pos(&config);
        if time % config.write_period < config.timestep {
            println!(
                "time: {} | Ball: [{}] | Bat [{}]",
                time.into_format_args(microsecond, Abbreviation),
                tt_ball.phys,
                bat.phys,
            );
        }
        time += config.timestep
    }


    // while time < config.duration {
    //     tt_ball.position[0] += tt_ball.velocity[0] * config.timestep;
    //     tt_ball.position[1] += tt_ball.velocity[1] * config.timestep;
    //     tt_ball.position[2] += tt_ball.velocity[2] * config.timestep;
    //     bat.position[0] += bat.velocity[0] * config.timestep;
    //     bat.position[1] += bat.velocity[1] * config.timestep;
    //     bat.position[2] += bat.velocity[2] * config.timestep;
    //     if config.duration % config.write_period < Time::new::<second>(1e-6) {
    //         println!("time: {} | ball-pos: {} | ball-speed {}", time, tt_ball.position, tt_ball.velocity);
    //     }
    //     if ((bat.position[0] - tt_ball.position[0]) < (config.timestep.get::<nanosecond>() * bat.velocity.get::<meter_per_nanosecond>())) 
    //     & ((bat.position[1] - tt_ball.position[1]) < (config.timestep.get::<nanosecond>() * bat.velocity.get::<meter_per_nanosecond>())) 
    //     & ((bat.position[2] - tt_ball.position[2]) < (config.timestep.get::<nanosecond>() * bat.velocity.get::<meter_per_nanosecond>())) {
    //         let momentum: Vec<Momentum> = vec![
    //             Momentum::new::<kilogram_meter_per_second>(0.0), 
    //             Momentum::new::<kilogram_meter_per_second>(0.0), 
    //             Momentum::new::<kilogram_meter_per_second>(0.0)
    //         ];
    //         momentum[0] = bat.velocity[0] * bat.mass;
    //         momentum[1] = bat.velocity[1] * bat.mass;
    //         momentum[2] = bat.velocity[2] * bat.mass;
    //         tt_ball.velocity[0] = momentum[0] / tt_ball.mass;
    //         tt_ball.velocity[1] = momentum[1] / tt_ball.mass;
    //         tt_ball.velocity[2] = momentum[2] / tt_ball.mass;
    //     }
    //     time += config.timestep;
    // }
}
